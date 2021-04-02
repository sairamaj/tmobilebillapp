using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using SelfService.Server.Model;
using SelfService.Shared;

namespace SelfService.Server.Repository
{
    class BillsRepository : IBillsRepository
    {
        private readonly HttpClient http;
        ApiUrl _apiUrl;
        public BillsRepository(IOptions<ApiUrl> apiUrlOptions, HttpClient http)
        {
            if (apiUrlOptions is null)
            {
                throw new System.ArgumentNullException(nameof(apiUrlOptions));
            }

            if (apiUrlOptions.Value is null)
            {
                throw new System.ArgumentNullException("apiUrls");
            }

            this._apiUrl = apiUrlOptions.Value;
            this.http = http ?? throw new ArgumentNullException(nameof(http));
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await GetBillsFromApi();
        }

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
            return await this.GetPrimaryContactsFromApi();
        }
        public async Task<Link> GetDownloadLink(string yearMonth)
        {
            return await this.GetDownloadUrlFromApi(yearMonth);
        }

        private async Task<IEnumerable<Bill>> GetBillsFromApi()
        {
            // GetFromJsonAsync fron Json extension cannot convert string to decimals.
            // Going back to Newtonsoft.Json Api.
            var response = await this.http.GetAsync(this._apiUrl.BillsUrl);
            response.EnsureSuccessStatusCode();
            return JsonConvert.DeserializeObject<IEnumerable<Bill>>(await response.Content.ReadAsStringAsync());
        }


        private async Task<IEnumerable<BillDetail>> GetBillDetailsFromApi(string yearMonth)
        {
            var response = await this.http.GetAsync(string.Format(this._apiUrl.DetailsUrl, yearMonth));
            response.EnsureSuccessStatusCode();
            return JsonConvert.DeserializeObject<IEnumerable<BillDetail>>(await response.Content.ReadAsStringAsync());
        }

        private async Task<IEnumerable<PrimaryContact>> GetPrimaryContactsFromApi()
        {
            return await this.http.GetFromJsonAsync<IEnumerable<PrimaryContact>>(this._apiUrl.Users);
        }

        private async Task<Link> GetDownloadUrlFromApi(string yearMonth)
        {
            System.Console.WriteLine($"--- DownloadLink-Api:" + string.Format(this._apiUrl.GetDownloadUrl, yearMonth));
           return await this.http.GetFromJsonAsync<Link>(string.Format(this._apiUrl.GetDownloadUrl, yearMonth));
        }
    }
}