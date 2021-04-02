using System;
using System.Threading.Tasks;

namespace SelfService.Shared
{
    public class NoOpCacheManager : ICacheManager
    {
        public async Task<T> GetWithSet<T>(string key, TimeSpan expiry, Func<Task<T>> func)
        {
            Console.WriteLine($"No op cache manager:{key}");
            return await func();
        }
    }
}