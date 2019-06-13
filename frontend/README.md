# Frontend
## General
Developed with the _[apache cordova](https://cordova.apache.org/)_ framework for different platforms.  
External libraries:
 - _[cordova-plugin-qrscanner](https://github.com/bitpay/cordova-plugin-qrscanner)_
 - _[cordova-plugin-qrcodejs](https://github.com/MenelicSoftware/cordova-plugin-qrcodejs.git)_
 - _[cordova-plugin-dialogs](https://github.com/apache/cordova-plugin-dialogs)_
 - _[jquery version 2.x](https://code.jquery.com/jquery/)_
 - _[jquery-mobile](https://jquerymobile.com/)_
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
USB-Debugging must be enabled on mobile device.


