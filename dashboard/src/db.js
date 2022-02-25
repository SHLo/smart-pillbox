import { CosmosClient } from "@azure/cosmos";

const endpoint = process.env.REACT_APP_DB_ENDPOINT;
const key = process.env.REACT_APP_DB_KEY;

const client = new CosmosClient({ endpoint, key });
const container = client.database("SmartPillbox").container("users");

async function getUsers() {
  const { resources } = await container.items
    .query(`SELECT * from users`)
    .fetchAll();

  const ret = {};

  for (let user of resources) {
    ret[user.tray] = user;
  }

  return ret;
}

async function updateUser(user) {
  const { id } = user;
  await container.item(id, id).replace(user);
  console.log(id, user);
}

export { getUsers, updateUser };
