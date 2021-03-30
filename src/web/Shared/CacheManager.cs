using System;
using System.Threading.Tasks;
using Blazored.LocalStorage;
using web.Shared.Model;

namespace web.Shared
{
    internal class CacheManager : ICacheManager
    {
        public CacheManager(ILocalStorageService service)
        {
            if (service is null)
            {
                throw new ArgumentNullException(nameof(service));
            }

            Service = service;
        }

        public ILocalStorageService Service { get; }

        public async Task<T> GetWithSet<T>(string key, TimeSpan expiry, Func<Task<T>> func)
        {
            var cacheEntry = await this.Service.GetItemAsync<CacheEntry<T>>(key);
            if( cacheEntry != null )
            {
                Console.WriteLine($"{key} Found in cache  expiry:{cacheEntry}");
                var timeSpan = DateTime.Now - cacheEntry.EntryTime;
                Console.WriteLine($"{key} Found in cache  expiry:{timeSpan.TotalSeconds}");
                if(timeSpan < expiry){
                    Console.WriteLine($"{key} Returning from cache");
                    return cacheEntry.Value;
                }
                else{
                    Console.WriteLine($"Expired in {key}");
                }
            }

            Console.WriteLine($"{key} Retriving from Source...");
            var val = (T)await func();

            Console.WriteLine($"{key} Setting in Cache:{val}");
            await this.Service.SetItemAsync<CacheEntry<T>>(key, new CacheEntry<T>{
                EntryTime = DateTime.Now,
                Expiry = expiry,
                Value = val
            });
            return val;
        }
    }
}