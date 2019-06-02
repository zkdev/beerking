# Frontend
## General
Developed with the _apache cordova_ framework for different platforms.  
External libraries:
 - _[cordova-plugin-qrscanner](https://github.com/bitpay/cordova-plugin-qrscanner)_
 - _[cordova-plugin-qrcodejs](https://github.com/MenelicSoftware/cordova-plugin-qrcodejs.git)_
 - _jquery_
 - _[md5](https://github.com/blueimp/JavaScript-MD5)_
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

