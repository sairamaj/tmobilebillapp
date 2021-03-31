invoke-restmethod https://9roffaomve.execute-api.us-west-2.amazonaws.com/Prod/api/phone/users | Format-List
read-host "running bills"
invoke-restmethod http://localhost:3000/api/phone/bills | Format-List
read-host "running bill details"
invoke-restmethod http://localhost:3000/api/phone/bills/Apr2020 | Format-List
invoke-restmethod https://9roffaomve.execute-api.us-west-2.amazonaws.com/Prod/api/phone/links/bills/Apr2020 | Format-List
