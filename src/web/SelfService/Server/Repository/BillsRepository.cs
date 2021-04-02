using System;
using System.Collections.Generic;
using System.Net.Http;
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

            if(apiUrlOptions.Value is null){
                throw new System.ArgumentNullException("apiUrls");
            }

            this._apiUrl = apiUrlOptions.Value;
            this.http = http ?? throw new ArgumentNullException(nameof(http));
        }
        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await GetBillsFromApi();
        }

        private async Task<IEnumerable<Bill>> GetBillsFromApi()
        {
            var response = await this.http.GetAsync(this._apiUrl.BillsUrl);
            response.EnsureSuccessStatusCode();
            return JsonConvert.DeserializeObject<IEnumerable<Bill>>(await response.Content.ReadAsStringAsync());
        }
    }
}