
const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb://mavyumnam_db_user:6he7SrKkQdqLpEZD@ac-ueqik67-shard-00-00.atrdmtd.mongodb.net:27017,ac-ueqik67-shard-00-01.atrdmtd.mongodb.net:27017,ac-ueqik67-shard-00-02.atrdmtd.mongodb.net:27017/?ssl=true&replicaSet=atlas-jtlga2-shard-0&authSource=admin&appName=Wahanthok";

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function run() {
  try {
    // Connect the client to the server	(optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);
