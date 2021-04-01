using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using web.Shared;
using web.Shared.Model;

namespace web.Repository
{
    internal class BillRepository : IBillRepository
    {
        private readonly ICacheManager cacheManager;
        private readonly ISettingsProvider settingsProvider;

        public BillRepository(
            HttpClient httpClient,
            ICacheManager cacheManager,
            ISettingsProvider settingsProvider)
        {
            if (httpClient is null)
            {
                throw new System.ArgumentNullException(nameof(httpClient));
            }

            if (cacheManager is null)
            {
                throw new System.ArgumentNullException(nameof(cacheManager));
            }

            this.HttpClient = httpClient;
            this.cacheManager = cacheManager;
            this.settingsProvider = settingsProvider ?? throw new System.ArgumentNullException(nameof(settingsProvider));
        }

        public HttpClient HttpClient { get; }

        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            var users = await this.GetUsers();
            var primaryUsers = await this.GetPrimaryContacts();
            return (await GetBillDetailsFromApi(yearMonth)).Select(b =>
            {
                var foundUser = users.FirstOrDefault(u => u.Phone == b.Number);
                if (foundUser != null)
                {
                    // Fill user name and primary user for this bill detail.
                    b.Name = foundUser.Name;
                    var foundPrimaryUser = primaryUsers.FirstOrDefault(p => p.Users.Any(u => u.Name == b.Name));
                    if (foundPrimaryUser != null)
                    {
                        b.Primary = foundPrimaryUser.Primary;
                    }
                }
                else
                {
                    b.Name = "Not Found";
                    b.Primary = "Primary not found";
                }

                return b;
            });
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.cacheManager.GetWithSet<IEnumerable<Bill>>(
                "bills",
                Constants.BillCacheExpiry,
                async () =>
            {
                return await this.HttpClient.GetFromJsonAsync<IEnumerable<Bill>>(this.settingsProvider.GetBillsUrl());
            });
        }

        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            return await this.cacheManager.GetWithSet<IEnumerable<PrimaryContact>>(
                "primary-contacts",
                Constants.UsersCacheExpiry,
                async () =>
            {
                return await this.HttpClient.GetFromJsonAsync<IEnumerable<PrimaryContact>>(this.settingsProvider.GetUserUrl());
            });
        }

        public async Task<IEnumerable<User>> GetUsers()
        {
            return (await GetPrimaryContacts()).SelectMany(p =>
            {
                return p.Users.Select(u =>
                {
                    u.Primary = p.Primary;
                    return u;
                });
            });
        }

        public async Task<string> GetDownloadLink(string yearMonth)
        {
            var linkDetails = await this.cacheManager.GetWithSet<Link>(
                $"bill-download-link-{yearMonth}",
                Constants.DownloadUrlCacheExpiry,
                async () =>
            {
                return await this.HttpClient.GetFromJsonAsync<Link>(this.settingsProvider.GetDownloadUrl(yearMonth));
            });

            return linkDetails.Url;
        }

        private async Task<IEnumerable<BillDetail>> GetBillDetailsFromApi(string yearMonth)
        {
            return await this.cacheManager.GetWithSet<IEnumerable<BillDetail>>(
                $"bill-details-{yearMonth}",
                Constants.BillDetailsCacheExpiry,
                async () =>
           {
               return await this.HttpClient.GetFromJsonAsync<IEnumerable<BillDetail>>(this.settingsProvider.GetBillDetailsUrl(yearMonth));
           });
        }
    }
}