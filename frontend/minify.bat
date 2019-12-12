@echo off
::css minifying
call postcss platforms/browser/www/css/friends.css > platforms/browser/www/css/friends_mini.css
call postcss platforms/browser/www/css/game.css > platforms/browser/www/css/game_mini.css
call postcss platforms/browser/www/css/index.css > platforms/browser/www/css/index_mini.css
call postcss platforms/browser/www/css/leaderboard.css > platforms/browser/www/css/leaderboard_mini.css
call postcss platforms/browser/www/css/main_page.css > platforms/browser/www/css/main_page_mini.css
call postcss platforms/browser/www/css/profile.css > platforms/browser/www/css/profile_mini.css
xcopy platforms\browser\www\css\profile_mini.css platforms\browser\www\css\profile.css /y
xcopy platforms\browser\www\css\main_page_mini.css platforms\browser\www\css\main_page.css /y
xcopy platforms\browser\www\css\leaderboard_mini.css platforms\browser\www\css\leaderboard.css /y
xcopy platforms\browser\www\css\index_mini.css platforms\browser\www\css\index.css /y
xcopy platforms\browser\www\css\game_mini.css platforms\browser\www\css\game.css /y
xcopy platforms\browser\www\css\friends_mini.css platforms\browser\www\css\friends.css /y
DEL platforms\browser\www\css\*_mini.css
@echo CSS Minified - Going on with JS
call javascript-obfuscator "./platforms/browser/www/js/friends.js" --output "./platforms/browser/www/js/friends.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/CreateAccount.js" --output "./platforms/browser/www/js/CreateAccount.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/game.js" --output "./platforms/browser/www/js/game.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/index.js" --output "./platforms/browser/www/js/index.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/login.js" --output "./platforms/browser/www/js/login.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/main.js" --output "./platforms/browser/www/js/main.js" --config "./minify_config.json"
call javascript-obfuscator "./platforms/browser/www/js/profile.js" --output "./platforms/browser/www/js/profile.js" --config "./minify_config.json"
@echo JS Minified - Going on with HTML
call html-minifier --input-dir "./platforms/browser/www"  --collapse-whitespace --remove-comments --remove-optional-tags --remove-redundant-attributes --remove-script-type-attributes --remove-tag-whitespace --output-dir "./platforms/browser/www" --file-ext html