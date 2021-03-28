using System.Collections.Generic;
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
            return await this.HttpClient.GetFromJsonAsync<BillDetail[]>(UrlConstants.GetBillDetailsUrl(yearMonth));
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.HttpClient.GetFromJsonAsync<Bill[]>(UrlConstants.BillsUrl);
        }

        public async Task<IEnumerable<User>> GetUsers()
        {
            return await Task.FromResult<IEnumerable<User>>(new List<User>{
                new User{
                    Name = "User-1",
                    PhoneNumber = "(503) 111-1111"
                }
            });
        }
    }
}