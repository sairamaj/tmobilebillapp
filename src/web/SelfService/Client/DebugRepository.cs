using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Client.Repository
{
    internal class DebugRepository : IDebugRepository
    {
        private readonly IHttpClientFactory clientFactory;

        public DebugRepository(IHttpClientFactory clientFactory)
        {
            this.clientFactory = clientFactory ?? throw new ArgumentNullException(nameof(clientFactory));
        }

        private HttpClient Client
        {
            get
            {
                return this.clientFactory.CreateClient("TMobile.ServerAPI");
            }
        }

        public async Task<DebugInfo> GetDebugInfo()
        {
            return await this.Client.GetFromJsonAsync<DebugInfo>($"/api/debug");
        }
    }
}