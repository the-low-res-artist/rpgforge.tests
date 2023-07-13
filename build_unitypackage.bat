:: =================================================================================================
:: Setup constants
set ROOT_PATH=%~dp0
set UNITY_EXE=C:\Program Files\Unity\Hub\Editor\2021.3.25f1\Editor\Unity.exe
set TEST_PROJECT_ROOT_PATH=%ROOT_PATH%Unity_test_runner
set TEST_PKG_NAME=RPGPowerForgeUnityTestRunner.unitypackage

:: =================================================================================================
:: Clear previous package if exists
if exist %TEST_PKG_NAME%.unitypackage del %TEST_PKG_NAME%
if exist "%TEST_PROJECT_ROOT_PATH%\%TEST_PKG_NAME%" del "%TEST_PROJECT_ROOT_PATH%\%TEST_PKG_NAME%"

:: =================================================================================================
:: Build package
set OPTIONS=-projectPath "%TEST_PROJECT_ROOT_PATH%" -exportPackage Assets\Tests %TEST_PKG_NAME% -quit
"%UNITY_EXE%" %ARGS%

:: =================================================================================================
:: Move the package in the root dir
move "%TEST_PROJECT_ROOT_PATH%\%TEST_PKG_NAME%" %TEST_PKG_NAME%

:: =================================================================================================
:: export to github
git add .
git commit -m "build + push automatic"
git push