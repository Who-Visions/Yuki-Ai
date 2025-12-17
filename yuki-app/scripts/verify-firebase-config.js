const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '../src/config/firebaseConfig.ts');

try {
    const content = fs.readFileSync(configPath, 'utf8');

    const expectedKeys = {
        apiKey: "AIzaSyBphgcHEYhOdMvAPceFVh8p-0QE_v1L12o",
        authDomain: "yuki-app-prod.firebaseapp.com",
        projectId: "yuki-app-prod",
        storageBucket: "yuki-app-prod.firebasestorage.app",
        messagingSenderId: "428249878686",
        appId: "1:428249878686:web:bc538526383564d2abab8f",
        measurementId: "G-GW1309B832"
    };

    let allFound = true;
    for (const [key, value] of Object.entries(expectedKeys)) {
        // Look for key: "value" or key: 'value'
        const pattern = new RegExp(`${key}\\s*:\\s*["']${value}["']`);
        if (!pattern.test(content)) {
            console.error(`❌ Missing or incorrect value for ${key}`);
            allFound = false;
        } else {
            console.log(`✅ Verified ${key}`);
        }
    }

    if (allFound) {
        console.log("SUCCESS: All Firebase configuration keys match production values.");
        process.exit(0);
    } else {
        console.error("FAILURE: Configuration mismatch.");
        process.exit(1);
    }

} catch (err) {
    console.error("Error reading file:", err);
    process.exit(1);
}
