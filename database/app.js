const { MongoClient } = require('mongodb');

// 1. Connection URL (Standard local computer address for MongoDB)
const url = 'mongodb://localhost:27017';
const client = new MongoClient(url);

// 2. Choose names for your database and collection
const dbName = 'dictionaryDB';
const collectionName = 'words';


async function main() {
    try {
        // Connect to the MongoDB Server
        await client.connect();
        console.log('Successfully connected to MongoDB server!');
        
        const db = client.db(dbName);
        const wordsCollection = db.collection(collectionName);

        // 3. Setup Indexes (Speeds up search dramatically)
        // This ensures lookups based on "lowercase_word" happen instantly
        await wordsCollection.createIndex({ lowercase_word: 1 });
        console.log('Database index created successfully.');

        // 4. Create Sample Dictionary Data
        const sampleWords = [
            {
                word: "Apple",
                lowercase_word: "apple",
                language: "en",
                part_of_speech: "noun",
                meanings: [
                    {
                        definition: "A round fruit with red, green, or yellow skin and crisp white flesh.",
                        examples: ["She took a bite out of a juicy red apple."]
                    }
                ]
            },
            {
                word: "Run",
                lowercase_word: "run",
                language: "en",
                part_of_speech: "verb",
                meanings: [
                    {
                        definition: "Move at a speed faster than a walk.",
                        examples: ["The children run around in the playground."]
                    },
                    {
                        definition: "Manage or be in charge of a business.",
                        examples: ["He runs a local grocery store."]
                    }
                ]
            }
        ];

        // 5. Insert Data into Database
        // We clean the collection first so you don't get duplicates if you run it twice
        await wordsCollection.deleteMany({}); 
        const insertResult = await wordsCollection.insertMany(sampleWords);
        console.log(`Inserted ${insertResult.insertedCount} words into the dictionary.`);

        // 6. Test Query: Lookup a word!
        const searchWord = "run";
        console.log(`\n--- Searching for the word: "${searchWord}" ---`);
        
        const foundWord = await wordsCollection.findOne({ lowercase_word: searchWord.toLowerCase() });

        if (foundWord) {
            console.log(`Word: ${foundWord.word} (${foundWord.part_of_speech})`);
            foundWord.meanings.forEach((meaning, index) => {
                console.log(`  Definition ${index + 1}: ${meaning.definition}`);
                console.log(`  Example: "${meaning.examples[0]}"`);
            });
        } else {
            console.log("Word not found in the dictionary.");
        }

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        // Always close the connection when finished
        await client.close();
        console.log('\nDatabase connection closed.');
    }
}

// Execute our program
main();
