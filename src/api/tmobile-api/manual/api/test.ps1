$Port = 6000
invoke-restmethod http://localhost:$Port/api/phone/users | Format-List
#read-host "running bills"
#invoke-restmethod http://localhost:$Port/api/phone/bills | Format-List
#read-host "running bill details"
#invoke-restmethod http://localhost:$Port/api/phone/bills/Apr2020 | Format-List
#invoke-restmethod http://localhost:$Port/api/phone/links/bills/Apr2020 | Format-List
invoke-restmethod http://localhost:$Port/api/phone/payments | Format-List
invoke-restmethod http://localhost:$Port/api/phone/payments/Jan2020 | Format-List
