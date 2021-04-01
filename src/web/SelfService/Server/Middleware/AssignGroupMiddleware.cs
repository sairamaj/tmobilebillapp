using System.Security.Claims;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using SelfService.Shared;

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
            this.logger.LogInformation($"InvokeAsync ...{context.User.GetEmail()}");
            if (IsAdmin(context.User.GetEmail()))
            {
                this.logger.LogInformation("Adding administrators role");
                ((ClaimsIdentity)context.User.Identity)
                        .AddClaim(new Claim(ClaimTypes.Role, "Administrators", ClaimValueTypes.String));
            }

            // Call the next delegate/middleware in the pipeline
            await next(context);
        }

        private bool IsAdmin(string email)
        {
            string[] currentAdmins = new string[] { "sairamaj@gmail.com", "srijamalapuram@gmail.com","radhachandra@gmail.com","rchandra02@outlook.com" };
            return currentAdmins.Contains(email);
        }
    }
}