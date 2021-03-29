https://docs.microsoft.com/en-us/aspnet/core/blazor/security/webassembly/standalone-with-azure-active-directory-b2c?view=aspnetcore-5.0

https://sairamaapps.b2clogin.com
sairamaapps.onmicrosoft.com
https://localhost:5001/authentication/login-callback

appid: <appidhere>
user flow: <userflowher>

dotnet new blazorwasm -au IndividualB2C --aad-b2c-instance "{AAD B2C INSTANCE}" --client-id "{CLIENT ID}" --domain "{TENANT DOMAIN}" -o {APP NAME} -ssp "{SIGN UP OR SIGN IN POLICY}"

