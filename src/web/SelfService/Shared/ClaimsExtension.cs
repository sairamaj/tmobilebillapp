using System;
using System.Linq;
using System.Security.Claims;

namespace SelfService.Shared
{
    public static class ClaimsExtension
    {
        public static string GetName(this ClaimsPrincipal principal)
        {
            if (principal == null)
            {
                return "NA";
            }

            var nameClaim = principal.Claims.FirstOrDefault(c => c.Type == "name");
            return nameClaim == null ? "unknown" : nameClaim.Value;
        }

        public static string GetEmail(this ClaimsPrincipal principal)
        {
            if (principal == null)
            {
                return "NA";
            }

            // foreach(var x in principal.Claims){
            //     System.Console.WriteLine($"{x.Type} : {x.Value}");
            // }

            var emaliClaim = principal.Claims.FirstOrDefault(c => c.Type == "emails");
            return emaliClaim == null ? "unknown" : emaliClaim.Value;
        }

        public static string GetId(this ClaimsPrincipal principal)
        {
            if (principal == null)
            {
                throw new ArgumentException($"Id not found in claims.");
            }

            foreach (var x in principal.Claims)
            {
                System.Console.WriteLine($"{x.Type} : {x.Value}");
            }

            var idClaim = principal.Claims.FirstOrDefault(c => c.Type == "http://schemas.microsoft.com/identity/claims/objectidentifier");
            if( idClaim == null){
                throw new ArgumentException($"http://schemas.microsoft.com/identity/claims/objectidentifier not found.");
            }

            return idClaim.Value;
        }

        public static string GetValue(this ClaimsPrincipal principal, string claimType)
        {
            if (principal == null)
            {
                throw new ArgumentException($"Id not found in claims.");
            }

            foreach (var x in principal.Claims)
            {
                System.Console.WriteLine($"{x.Type} : {x.Value}");
            }

            var idClaim = principal.Claims.FirstOrDefault(c => c.Type == claimType);
            if( idClaim == null){
                throw new ArgumentException($"{claimType} not found.");
            }

            return idClaim.Value;
        }

    }
}