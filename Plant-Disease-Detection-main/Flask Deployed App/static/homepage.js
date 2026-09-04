// Import Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore, getDoc, doc } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "login-form-64b0e.firebaseapp.com",
    projectId: "login-form-64b0e",
    storageBucket: "login-form-64b0e.firebasestorage.app",
    messagingSenderId: "445730795305",
    appId: "1:445730795305:web:68c261387381869f881138",
    measurementId: "G-BDJCDVGYX3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
const db = getFirestore();

// Check user authentication status
onAuthStateChanged(auth, (user) => {
    const loggedInUserId = localStorage.getItem('loggedInUserId');

    if (user && loggedInUserId) {
        const docRef = doc(db, "users", loggedInUserId);
        getDoc(docRef)
            .then((docSnap) => {
                if (docSnap.exists()) {
                    const userData = docSnap.data();
                    document.getElementById('loggedUserFName').innerText = userData.firstName;
                    document.getElementById('loggedUserLName').innerText = userData.lastName;
                    document.getElementById('loggedUserEmail').innerText = userData.email;
                } else {
                    console.log("No document found for the user.");
                }
            })
            .catch((error) => {
                console.error("Error fetching user document:", error);
            });
    } else {
        console.log("User is not logged in or missing user ID.");
        window.location.href = '/'; // Redirect to login page
    }
});

// Logout functionality
const logoutButton = document.getElementById('logout');
logoutButton.addEventListener('click', () => {
    localStorage.removeItem('loggedInUserId');
    signOut(auth)
        .then(() => {
            window.location.href = '/'; // Redirect to login
        })
        .catch((error) => {
            console.error('Error signing out:', error);
        });
});
