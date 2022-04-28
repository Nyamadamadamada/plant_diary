import { initializeApp } from "firebase/app";
import { getStorage, ref, uploadBytes } from "firebase/storage";
import { getAuth, signOut, signInWithEmailAndPassword } from "firebase/auth";
import { config } from "../config/firebaes_config.js";
import fs from "fs";
import "date-utils";

const firebaseConfig = {
  apiKey: config.firebaseConfig.apiKey,
  authDomain: config.firebaseConfig.authDomain,
  projectId: config.firebaseConfig.projectId,
  storageBucket: config.firebaseConfig.storageBucket,
  messagingSenderId:config.firebaseConfig.messagingSenderId,
  appId: config.firebaseConfig.appId,
  measurementId: config.firebaseConfig.measurementId
};
const PTHOTO_PATH = config.ROOT_PATH + 'workspace/taken/photo.jpg';
const STORE_PATH = config.ROOT_PATH + 'workspace/store/';

const now = new Date().toFormat("YYYYMMDDHH24MISS");
const file_name = config.GROWING_PLANT_CODE + '_' + now + '.jpg';
const upFilePath = STORE_PATH + file_name;
const firebaseApp = initializeApp(firebaseConfig);
const storage = getStorage(firebaseApp);
const storageRef = ref(storage, upFilePath);
const auth = getAuth();

function callback(err) {
    if (err) throw err;
    // Storageに送信
    signInWithEmailAndPassword(auth, config.auth.email, config.auth.password)
    .then(() => {
    console.log('Firebaseログイン成功');
    fs.readFile(upFilePath, (error, file) => {
        if (error) {
            console.error(error);
        } else {
            uploadBytes(storageRef, file)
                .then((snapshot) => {
                    signOut(auth).then(() => {
                            console.log('Firebaseログアウト');
                        }).catch((error) => {
                            console.log(error);
                        });
                });
        }
    });
    })
    .catch((error) => {
        console.log(error.message);
    });
}
  
fs.copyFile(PTHOTO_PATH, STORE_PATH + file_name, callback);
  
