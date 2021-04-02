using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Client.Repository
{
    internal class BillsRepository : IBillRepository
    {
        private readonly HttpClient http;
        private readonly ICacheManager cacheManager;

        public BillsRepository(HttpClient http, ICacheManager cacheManager)
        {
            this.http = http ?? throw new System.ArgumentNullException(nameof(http));
            this.cacheManager = cacheManager ?? throw new System.ArgumentNullException(nameof(cacheManager));
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.cacheManager.GetWithSet<IEnumerable<Bill>>(
                           "bills",
                           Constants.BillCacheExpiry,
                           async () =>
                       {
                           return await this.http.GetFromJsonAsync<IEnumerable<Bill>>("/api/bills");
                       });
        }
    }
}