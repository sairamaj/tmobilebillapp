using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System;
using System.Linq;
using SelfService.Shared;

namespace SelfService.Server.Controllers
{
    [Authorize(Roles = "Users")]
    [ApiController]
    [Route("[controller]")]
    public class DebugController
    {
        public DebugController(IHttpClientFactory clientFactory)
        {
            this.ClientFactory =
                clientFactory ?? throw new ArgumentNullException(nameof(clientFactory));
        }

        public IHttpClientFactory ClientFactory { get; }

        [HttpGet]
        [Route("/api/debug")]
        public Task<DebugInfo> GetDebugInfo()
        {
            var client = this.ClientFactory.CreateClient("t-mobile-api");

            var apiKey = "NA";
            if (client.DefaultRequestHeaders.TryGetValues("x-api-key", out var values))
            {
                apiKey = values.FirstOrDefault();
            }

            var debugInfo = new DebugInfo
            {
                ApiBaseAddress = client.BaseAddress.ToString(),
                ApiKey = Mask(apiKey),
            };

            return Task.FromResult<DebugInfo>(debugInfo);
        }

        private string Mask(string val)
        {
			// show first 3 and last 3
			if(string.IsNullOrWhiteSpace(val)){
				return "<null>";
			}

			if(val.Length < 6){
				return val;
			}

			var mask = val.Substring(0,3);
			mask += new string('*',val.Length-6);
			mask += val.Substring(val.Length-3,3);
            return mask;
        }
    }
}
