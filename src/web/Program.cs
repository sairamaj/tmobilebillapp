using System;
using System.Net.Http;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using MatBlazor;
using web.Repository;
using Microsoft.Extensions.Caching.Memory;
using web.Shared;
using Blazored.LocalStorage;

namespace web
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");

            builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
            builder.Services.AddSingleton<IMemoryCache, MemoryCache>();
            builder.Services.AddScoped<ICacheManager, CacheManager>();
            builder.Services.AddScoped<IBillRepository, BillRepository>();
            //  builder.Services.AddScoped<IBillRepository, FakeBillRepository>();
            builder.Services.AddMatBlazor();
            builder.Services.AddBlazoredLocalStorage(config =>
                    config.JsonSerializerOptions.WriteIndented = true);
            await builder.Build().RunAsync();
        }
    }
}
