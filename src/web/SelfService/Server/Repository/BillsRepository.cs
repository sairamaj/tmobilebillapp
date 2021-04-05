using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;
using SelfService.Shared;

namespace SelfService.Server.Repository
{
    internal class BillsRepository : IBillsRepository
    {
        private readonly IHttpClientFactory clientFactory;
        private readonly ICacheManager cacheManager;
        public BillsRepository(
            IHttpClientFactory clientFactory,
            ICacheManager cacheManager)
        {
            this.clientFactory = clientFactory ?? throw new ArgumentNullException(nameof(clientFactory));
            this.cacheManager = cacheManager ?? throw new ArgumentNullException(nameof(cacheManager));
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.cacheManager.GetWithSet<IEnumerable<Bill>>(
                           "bills",
                           Constants.BillCacheExpiry,
                           async () =>
                       {
                           return await GetBillsFromApi();
                       });
        }

        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            return await this.cacheManager.GetWithSet<IEnumerable<BillDetail>>(
                        $"bills-details-{yearMonth}",
                        Constants.BillDetailsCacheExpiry,
                        async () =>
                    {
                        return await this.GetBillDetailsInternal(yearMonth);
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

        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            return await this.cacheManager.GetWithSet<IEnumerable<PrimaryContact>>(
                          $"primary-contacts",
                          Constants.UsersCacheExpiry,
                          async () =>
                      {
                          return await this.GetPrimaryContactsFromApi();
                      });
        }
        public async Task<Link> GetDownloadLink(string yearMonth)
        {
            return await this.cacheManager.GetWithSet<Link>(
                           $"bills-download-url-{yearMonth}",
                           Constants.BillDetailsCacheExpiry,
                           async () =>
                       {
                           return await this.GetDownloadUrlFromApi(yearMonth);
                       });
        }

        public async Task<IDictionary<string, Role>> GetUserRoles()
        {
            return await this.cacheManager.GetWithSet<IDictionary<string, Role>>(
                           "userroles",
                           Constants.UserRolesCacheExpiry,
                           async () =>
                       {
                           return await this.GetUserRolesFromApi();
                       });
        }

        private HttpClient Client
        {
            get
            {
                return this.clientFactory.CreateClient("t-mobile-api");
            }
        }

        private async Task<IEnumerable<BillDetail>> GetBillDetailsInternal(string yearMonth)
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
        private async Task<IEnumerable<Bill>> GetBillsFromApi()
        {
            // GetFromJsonAsync fron Json extension cannot convert string to decimals.
            // Going back to Newtonsoft.Json Api.
            System.Console.WriteLine($"--- GetBillsFrom-Api:");
            foreach (var h in this.Client.DefaultRequestHeaders)
            {
                System.Console.WriteLine("-----------------------");
                System.Console.WriteLine($"{h.Key}:{h.Value.First()}");
                System.Console.WriteLine("-----------------------");
            }
            var response = await this.Client.GetAsync("bills");
            response.EnsureSuccessStatusCode();
            return JsonConvert.DeserializeObject<IEnumerable<Bill>>(await response.Content.ReadAsStringAsync());
        }

        private async Task<IEnumerable<BillDetail>> GetBillDetailsFromApi(string yearMonth)
        {
            System.Console.WriteLine($"--- GetBillDetailsFrom-Api:" + yearMonth);
            var response = await this.Client.GetAsync($"bills/{yearMonth}");
            response.EnsureSuccessStatusCode();
            return JsonConvert.DeserializeObject<IEnumerable<BillDetail>>(await response.Content.ReadAsStringAsync());
        }

        private async Task<IEnumerable<PrimaryContact>> GetPrimaryContactsFromApi()
        {
            System.Console.WriteLine($"--- GetPrimaryContactsFrom-Api:");
            return await this.Client.GetFromJsonAsync<IEnumerable<PrimaryContact>>("users");
        }

        private async Task<Link> GetDownloadUrlFromApi(string yearMonth)
        {
            System.Console.WriteLine($"--- DownloadLink-Api:" + yearMonth);
            return await this.Client.GetFromJsonAsync<Link>($"links/bills/{yearMonth}");
        }

        private async Task<IDictionary<string, Role>> GetUserRolesFromApi()
        {
            System.Console.WriteLine($"--- User roles -Api:");
            // return await this.Client.GetFromJsonAsync<IDictionary<string,Role>>($"userroles");
            await Task.Delay(0);
            var roles = (JsonConvert.DeserializeObject<IEnumerable<Role>>(System.IO.File.ReadAllText(@"c:\temp\userroles.json")));
            return new Dictionary<string, Role>(roles.ToDictionary(r => r.Name, r => r), StringComparer.OrdinalIgnoreCase);
        }
    }
}