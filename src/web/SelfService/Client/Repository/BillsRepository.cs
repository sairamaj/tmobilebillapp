using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Client.Repository
{
    internal class BillsRepository : IBillsRepository
    {
        private readonly HttpClient http;
        private readonly ICacheManager cacheManager;

        public BillsRepository(HttpClient http, ICacheManager cacheManager)
        {
            this.http = http ?? throw new System.ArgumentNullException(nameof(http));
            this.cacheManager = cacheManager ?? throw new System.ArgumentNullException(nameof(cacheManager));
        }

        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<BillDetail>>(
                           $"bills-details-{yearMonth}",
                           Constants.BillDetailsCacheExpiry,
                           async () =>
                       {
                           return await this.http.GetFromJsonAsync<IEnumerable<BillDetail>>($"/api/bills/{yearMonth}");
                       });
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<Bill>>(
                           "bills",
                           Constants.BillCacheExpiry,
                           async () =>
                       {
                           return await this.http.GetFromJsonAsync<IEnumerable<Bill>>("/api/bills");
                       });
        }

        public async Task<Link> GetDownloadLink(string yearMonth)
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<Link>(
                           $"bills-download-url-{yearMonth}",
                           Constants.BillDetailsCacheExpiry,
                           async () =>
                       {
                           return await this.http.GetFromJsonAsync<Link>($"/api/links/bills/{yearMonth}");
                       });
        }

        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<PrimaryContact>>(
                          $"primary-contacts",
                          Constants.UsersCacheExpiry,
                          async () =>
                      {
                          return await this.http.GetFromJsonAsync<IEnumerable<PrimaryContact>>($"/api/primarycontacts");
                      });
        }

        public async Task<IEnumerable<User>> GetUsers()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<User>>(
                          $"users",
                          Constants.BillDetailsCacheExpiry,
                          async () =>
                      {
                          return await this.http.GetFromJsonAsync<IEnumerable<User>>($"/api/users");
                      });
        }

        // Temporary method till we implement full client authorization roles
        // This will throw Un authorized(403) if user is not authorized.
        public async Task EnsureAuthorized()
        {
            await this.http.GetFromJsonAsync<bool>("/api/authorized/state");
        }

        public Task<IDictionary<string, Role>> GetUserRoles()
        {
            throw new NotImplementedException("We dont need at client side now.");
        }
    }
}