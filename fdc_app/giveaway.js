import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.6.0/firebase-app.js';
import { getFirestore, collection, getDocs } from 'https://www.gstatic.com/firebasejs/9.6.0/firebase-firestore.js';

const firebaseApp = initializeApp({
	apiKey: "AIzaSyABMJ_QX2p9DitbmG67xBjJlKzc6biT7yY",
  authDomain: "frontierdirectcare.firebaseapp.com",
  databaseURL: "https://frontierdirectcare-default-rtdb.firebaseio.com",
  projectId: "frontierdirectcare",
  storageBucket: "frontierdirectcare.appspot.com",
  messagingSenderId: "568023875348",
  appId: "1:568023875348:web:5c1669ef43ad47ff7acc01",
  measurementId: "${config.measurementId}"
});

const db = getFirestore(firebaseApp);
const contestants = collection(db, 'contestant');
const snapshot = await getDocs(contestants);
console.log(snapshot);

document.querySelector('.form-select').addEventListener('change', function(e) {
	var route = Array.from(e.target.querySelectorAll('option')).filter(function(x) {
		return x.selected == true;
	});

	if(route[0].value == 'refer') {
		location.pathname = '/app/refer';
	}

	if(route[0].value == 'reason') {
		location.pathname = '/app';
	}
});