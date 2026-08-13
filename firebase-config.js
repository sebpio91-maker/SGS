// Trage hier die Werte aus deiner eigenen Firebase-Projekt-Konsole ein:
// Projekteinstellungen -> "Meine Apps" -> Web-App hinzufügen -> SDK-Konfiguration.
//
// Diese Werte sind KEIN Geheimnis. Die Firebase-Web-Konfiguration ist dafür
// gedacht, öffentlich im Browser-Code zu stehen -- Sicherheit kommt über die
// Firestore-/Storage-Regeln (firestore.rules / storage.rules), nicht über das
// Verstecken dieser Werte. Siehe README, Abschnitt "Hand-Chat einrichten".
export const firebaseConfig = {
  apiKey: 'DEIN_API_KEY',
  authDomain: 'DEIN_PROJEKT.firebaseapp.com',
  projectId: 'DEIN_PROJEKT',
  storageBucket: 'DEIN_PROJEKT.appspot.com',
  messagingSenderId: 'DEINE_SENDER_ID',
  appId: 'DEINE_APP_ID',
};
