using System.Security.Claims;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using SelfService.Shared;
using System.Collections.Generic;

namespace SelfService.Server.Middleware
{
    class AssignGroupMiddleware
    {
        private readonly RequestDelegate next;
        private readonly ILogger<AssignGroupMiddleware> logger;

        public AssignGroupMiddleware(RequestDelegate next, ILogger<AssignGroupMiddleware> logger)
        {
            this.next = next ?? throw new System.ArgumentNullException(nameof(next));
            this.logger = logger ?? throw new System.ArgumentNullException(nameof(logger));
        }

        public async Task InvokeAsync(HttpContext context)
        {
            await Task.Delay(0);
            foreach (var role in GetUserRoles(context.User.GetEmail()))
            {
                this.logger.LogInformation($"Adding role: {role}");
                ((ClaimsIdentity)context.User.Identity)
                        .AddClaim(new Claim(ClaimTypes.Role, role, ClaimValueTypes.String));
            }

            // Call the next delegate/middleware in the pipeline
            await next(context);
        }

        private IEnumerable<string> GetUserRoles(string email)
        {
            if (email == "unknown")
            {
                return new string[] { "Guest" };
            }

            this.logger.LogInformation($"Getting roles: {email}");
            if(email == "srijamalapuram@gmail.com")
            {
                return new string[] { "Users" };
            }
            
            return new string[] { "Guest" };
        }
    }
}