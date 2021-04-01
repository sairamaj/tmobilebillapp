using Microsoft.AspNetCore.Builder;

namespace SelfService.Server.Middleware
{
    internal static class AssignGroupMiddlewareExtensions
    {
        public static IApplicationBuilder UseAssignGroup(
                   this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<AssignGroupMiddleware>();
        }
    }
}