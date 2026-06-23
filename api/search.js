const { MongoClient } = require('mongodb');

// 1. Connection Caching: This lives outside the export function
let cachedClient = null;

async function getDatabase() {
    if (cachedClient) return cachedClient;
    // Ensure you have MONGODB_URI in your Vercel Environment Variables
    const client = new MongoClient(process.env.MONGODB_URI);
    await client.connect();
    cachedClient = client;
    return client;
}

// 2. The Request Handler: Your code goes here
module.exports = async (req, res) => {
    try {
        const { word } = req.query;
        if (!word) {
            return res.status(400).json({ error: "Missing word parameter" });
        }

        const client = await getDatabase();
        const result = await client.db("dictionaryDB").collection("words").findOne({ word: word });
        
        res.status(200).json(result || { message: "Word not found" });
    } catch (error) {
        console.error(error); // Helpful for debugging in Vercel logs
        res.status(500).json({ error: "Internal Server Error" });
    }
};