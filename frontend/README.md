# Frontend
## General
Developed with the _apache cordova_ framework for different platforms.  
Plugins in use:
 - _[cordova-plugin-qrscanner](https://github.com/bitpay/cordova-plugin-qrscanner)_
 - _[cordova-plugin-qrcodejs](https://github.com/MenelicSoftware/cordova-plugin-qrcodejs.git)_
 - _[cordova-plugin-password-crypto](https://github.com/blackberry/WebWorks-Community-APIs/tree/master/BB10-Cordova/PasswordCrypto)_
## Usage
### Installation
First install required node packages:
```
npm install
```

Create required platforms:
```
cordova platform add [browser|android|ios|...]
```
### Run
Run browser version on local browser:
```
cordova run browser
```
Run on your mobile android device:
```
cordova run android --device
```
USB-Debugging must be available on mobile device.

### __only for developing__: 
``` 
user:       test  
password:   test
```

