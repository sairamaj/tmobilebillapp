using System;
using System.Threading.Tasks;
using Blazored.LocalStorage;

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

        public async Task<T> GetWithSet<T>(string key, Func<Task<T>> func)
        {
            var item = await this.Service.GetItemAsync<T>(key);
            if(item != null){
                return item;
            }

            var val = (T)await func();

            await this.Service.SetItemAsync<T>(key, val);
            return val;
        }
    }
}