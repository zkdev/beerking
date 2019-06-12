cordova.define('cordova/plugin_list', function(require, exports, module) {
  module.exports = [
    {
      "id": "cordova-plugin-qrcodejs.QRCodeJS",
      "file": "plugins/cordova-plugin-qrcodejs/www/qrcodejsPlugin.js",
      "pluginId": "cordova-plugin-qrcodejs",
      "clobbers": [
        "cordova.plugins.qrcodejs"
      ]
    },
    {
      "id": "cordova-plugin-qrcodejs.QRCcodeJSImpl",
      "file": "plugins/cordova-plugin-qrcodejs/www/qrcode.js",
      "pluginId": "cordova-plugin-qrcodejs",
      "runs": true
    },
    {
      "id": "cordova-plugin-qrcodejs.QRCcodeJSProxy",
      "file": "plugins/cordova-plugin-qrcodejs/www/qrcodejsPluginProxy.js",
      "pluginId": "cordova-plugin-qrcodejs",
      "runs": true
    },
    {
      "id": "cordova-plugin-qrscanner.QRScanner",
      "file": "plugins/cordova-plugin-qrscanner/www/www.min.js",
      "pluginId": "cordova-plugin-qrscanner",
      "clobbers": [
        "QRScanner"
      ]
    },
    {
      "id": "cordova-plugin-dialogs.notification",
      "file": "plugins/cordova-plugin-dialogs/www/notification.js",
      "pluginId": "cordova-plugin-dialogs",
      "merges": [
        "navigator.notification"
      ]
    },
    {
      "id": "cordova-plugin-dialogs.notification_android",
      "file": "plugins/cordova-plugin-dialogs/www/android/notification.js",
      "pluginId": "cordova-plugin-dialogs",
      "merges": [
        "navigator.notification"
      ]
    }
  ];
  module.exports.metadata = {
    "cordova-plugin-qrcodejs": "1.0.0",
    "cordova-plugin-qrscanner": "3.0.1",
    "cordova-plugin-whitelist": "1.3.3",
    "cordova-plugin-dialogs": "2.0.1"
  };
});