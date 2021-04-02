using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Memory;
using SelfService.Shared;

namespace SelfService.Server.Repository
{
    internal class CacheManager : ICacheManager
    {
        private readonly IMemoryCache cache;

        public CacheManager(IMemoryCache cache)
        {
            this.cache = cache ?? throw new ArgumentNullException(nameof(cache));
        }

        public async Task<T> GetWithSet<T>(string key, TimeSpan expiry, Func<Task<T>> func)
        {
            if (cache.TryGetValue(key, out var val))
            {
                return (T)val;
            }

            var newVal = await func();

            var cacheEntryOptions = new MemoryCacheEntryOptions().SetSlidingExpiration(expiry);

            // Save data in cache.
            cache.Set(key, newVal, cacheEntryOptions);
            return newVal;
        }
    }
}