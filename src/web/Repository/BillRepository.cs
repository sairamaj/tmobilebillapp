using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using web.Shared.Model;

namespace web.Repository
{
    internal class BillRepository : IBillRepository
    {
        public BillRepository(HttpClient httpClient)
        {
            if (httpClient is null)
            {
                throw new System.ArgumentNullException(nameof(httpClient));
            }

            HttpClient = httpClient;
        }

        public HttpClient HttpClient { get; }

        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            var users = await this.GetUsers();
            return (await GetBillDetailsFromApi(yearMonth)).Select(b =>
            {
                var foundUser = users.FirstOrDefault(u => u.Phone == b.Number);
                if (foundUser != null)
                {
                    b.Name = foundUser.Name;
                }
                else
                {
                    b.Name = $"Not Found";
                }

                return b;
            });
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.HttpClient.GetFromJsonAsync<Bill[]>(UrlConstants.BillsUrl);
        }

        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            return await this.HttpClient.GetFromJsonAsync<PrimaryContact[]>(UrlConstants.UsersUrl);
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

        private async Task<IEnumerable<BillDetail>> GetBillDetailsFromApi(string yearMonth)
        {
            return await this.HttpClient.GetFromJsonAsync<BillDetail[]>(UrlConstants.GetBillDetailsUrl(yearMonth));
        }
    }
}