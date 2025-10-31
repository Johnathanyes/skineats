// firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// You can switch configs via environment variables later
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "your-app.firebaseapp.com",
  projectId: "your-app",
  storageBucket: "your-app.appspot.com",
  messagingSenderId: "000000000000",
  appId: "1:000000000000:web:abcdef123456"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);