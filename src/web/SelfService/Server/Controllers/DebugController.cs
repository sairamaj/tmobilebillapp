using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System;
using System.Linq;
using SelfService.Shared;

namespace SelfService.Server.Controllers
{
   // [Authorize(Roles = "Users")]
	[ApiController]
	[Route("[controller]")]
	public class DebugController
	{
		public DebugController(IHttpClientFactory clientFactory)
		{
			this.ClientFactory = clientFactory ?? throw new ArgumentNullException(nameof(clientFactory));
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
				ApiKey = apiKey,
			};

			return Task.FromResult<DebugInfo>(debugInfo);
		}
	}
}