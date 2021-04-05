using System.Security.Claims;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using SelfService.Shared;
using System.Collections.Generic;
using System;

namespace SelfService.Server.Middleware
{
    internal class AssignGroupMiddleware
    {
        private readonly RequestDelegate next;
        private readonly ILogger<AssignGroupMiddleware> logger;
        private readonly IBillsRepository repository;

        public AssignGroupMiddleware(
            RequestDelegate next, 
            ILogger<AssignGroupMiddleware> logger,
            IBillsRepository repository)
        {
            this.next = next ?? throw new System.ArgumentNullException(nameof(next));
            this.logger = logger ?? throw new System.ArgumentNullException(nameof(logger));
            this.repository = repository ?? throw new System.ArgumentNullException(nameof(repository));
        }

        public async Task InvokeAsync(HttpContext context)
        {
            await Task.Delay(0);
            foreach (var role in await GetUserRoles(context.User.GetEmail()))
            {
                this.logger.LogInformation($"Adding role: {role}");
                ((ClaimsIdentity)context.User.Identity)
                        .AddClaim(new Claim(ClaimTypes.Role, role, ClaimValueTypes.String));
            }

            // Call the next delegate/middleware in the pipeline
            await next(context);
        }

        private async Task<IEnumerable<string>> GetUserRoles(string email)
        {
            this.logger.LogInformation($"Querying role for user: {email}");
            if (email == "unknown")
            {
                return new string[] { "Guest" };
            }

            var roles = new List<string>();
            foreach(var role in await this.repository.GetUserRoles())
            {
                if( role.Value.Users.Contains(email, StringComparer.OrdinalIgnoreCase)){
                    roles.Add(role.Value.Name);
                }
            }

            return roles;
        }
    }
}