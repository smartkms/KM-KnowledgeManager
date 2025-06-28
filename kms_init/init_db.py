from pymilvus import __version__ as MILVUS_VERSION, MilvusClient, MilvusException, FieldSchema, CollectionSchema
from pymilvus.exceptions import *
from common.logger import getLogger
import yaml
from time import sleep

# TODO if old db still exists create Y/N option to drop it and create new, same for schemas
# TODO update mode for collection add config property milvus.update
# TODO print errors to logger
# TODO info for already existing users, roles, privilege_groups

CONFIG_FILE = 'milvus_init.yaml'

logger = getLogger("init-db")
logger.info("pymilvus version - %s", MILVUS_VERSION)

def create_collections(collections, client) :
    for collection_name, collection in collections.items():
        if client.has_collection(collection_name):
            logger.info("Collection %s already exists.", collection_name)
            continue
        try:
            try:
                schema_data = collection["schema"]
                fields = []
                for field in schema_data["fields"]:
                    field_schema = FieldSchema.construct_from_dict(field)
                    fields.append(field_schema.to_dict())
                schema_dict = {
                    "enable-dynamic-field": schema_data["enable-dynamic-field"],
                    "fields" : fields
                }
                schema = CollectionSchema.construct_from_dict(schema_dict)
            except MilvusException as e:
                logger.error("Could not create schema.")
                raise e
            try:
                index_params = MilvusClient.prepare_index_params()
                for index in collection["indexes"]:
                    if "vector" in index:
                        index_params.add_index(
                            field_name=index["field-name"],
                            index_type=index["type"],
                            index_name=index["name"],
                            metric_type=index["metric-type"],
                            params=index["params"]
                        )
                    else:
                        if "type" in index:
                            index_params.add_index(
                                field_name=index["field-name"],
                                index_type=index["type"],
                                index_name=index["name"]
                            )
                        else:
                            index_params.add_index(
                                field_name=index["field-name"],
                                index_name=index["name"]
                            )
            except MilvusException as e:
                logger.error("Could not initialize indexes.")
                raise e
            
            if "partitions" in collection:
                logger.warning("Creating partitions not yet supported")

            # TODO add mmap.enabled to properties
            try:
                if "partition-key-settings" in collection:
                    pks = collection["partition-key-settings"]
                    client.create_collection(
                        collection_name=collection_name,
                        schema=schema,
                        index_params=index_params,
                        num_partitions = pks["num-partitions"],
                        properties={"partitionkey.isolation": pks["partitionkey-isolation"]}
                    )
                else:
                    client.create_collection(
                        collection_name=collection_name,
                        schema=schema,
                        index_params=index_params
                    )
            except MilvusException as e:
                logger.error("Could not create collection %s", collection_name)
                raise e
            logger.info("Succcessfully created collection %s", collection_name)
        except PrimaryKeyException as e:
            logger.fatal("Schema for %s has no primary key.", collection_name)
            # raise MilvusException() TODO raise milvusException
        except MilvusException as e:
            client.drop_collection(collection_name)
            logger.fatal("Error during creation of collection %s.", collection_name)
            raise e

def create_privilege_groups(client, privilege_groups):
    for name, privileges in privilege_groups.items():
        try:
            if name in list(map(lambda d: d['privilege_group'], client.list_privilege_groups())):
                continue
            print(name in client.list_privilege_groups())
            client.create_privilege_group(group_name=name)
            try:
                client.add_privileges_to_group(group_name=name, privileges=privileges)
            except MilvusClient as e:
                client.drop_privilege_group(group_name=name)
                raise e
        except MilvusException as e:
            logger.fatal("Could not create privilege group %s: %s", name, e)

def create_roles(client, roles) :
    for role_name, privileges in roles.items():
        if role_name in client.list_roles():
            continue
        try:
            client.create_role(role_name=role_name)
            for privilege_name, scope in privileges["privileges"].items():
                try:
                    print(privilege_name)
                    print(scope)
                    client.grant_privilege_v2(
                        role_name=role_name,
                        privilege=privilege_name,
                        collection_name=scope["collection"],
                        db_name=scope["db"]
                    )        
                except MilvusException as e:
                    logger.fatal("Could not grant privilege: %s", privilege_name)
                    client.drop_role(role_name=role_name)
                    raise e
        except MilvusException as e:
            logger.fatal("Could not create role %s", role_name)

def create_users(client, users) :
    for user in users:
        if user["name"] in client.list_users():
            continue
        try:
            client.create_user(user_name=user["name"], password=user["password"])
            for role in user["roles"]:
                try:
                    client.grant_role(user_name=user["name"], role_name=role)
                except MilvusException as e:
                    logger.fatal("Could not grant role %s to user %s", role, user["name"])
        except MilvusException as e:
            logger.fatal("Could not create user %s", user["name"])


try:
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    milvus = config["milvus"]
    uri = milvus["uri"]
    token = milvus["token"]
    try:
        client =  MilvusClient(uri=uri, token=token)
        # print(client.list_users())
        # for name in client.list_users():
        #     if name=="root":
        #         continue
        #     client.drop_user(name)
        # print(client.list_roles())
        # for name in client.list_roles():
        #     if name =="admin":
        #         continue
        #     client.drop_privilege_group(name)
        # print(client.list_privilege_groups())
        # for name in client.list_privilege_groups():
        #     client.drop_privilege_group(name)
        for database_name, database in milvus["databases"].items():
            if not database_name in client.list_databases():
                client.create_database(database_name)
            client.using_database(database_name)
            create_collections(database["collections"], client=client)
        create_privilege_groups(client=client, privilege_groups=milvus["privilege-groups"])
        create_roles(client=client, roles=milvus["roles"])
        create_users(client=client, users=milvus["users"])
        client.update_password(
            user_name="root",
            old_password=milvus["password"],
            new_password=milvus["new-password"]
        )
    except MilvusException as e:
        logger.fatal("Error creating milvus client: %s", e)
    finally:
        client.close()
    client.close()
except FileNotFoundError:
    logger.fatal("Error: %s not found.", CONFIG_FILE)
except yaml.YAMLError as e:
    logger.fatal("Error: Invalid YAML format - %s", e)
except KeyError as e:
    logger.fatal("Error: Missing key in configuration - %s", e)



