using System;
using System.Net.Http;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text;
using Microsoft.AspNetCore.Components.WebAssembly.Authentication;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using MatBlazor;
using Blazored.LocalStorage;
using SelfService.Client.Repository;
using SelfService.Shared;

namespace SelfService.Client
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("app");

            builder.Services.AddHttpClient("SelfService.ServerAPI", client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress))
                .AddHttpMessageHandler<BaseAddressAuthorizationMessageHandler>();

            // Supply HttpClient instances that include access tokens when making requests to the server project
            builder.Services.AddTransient(sp => sp.GetRequiredService<IHttpClientFactory>().CreateClient("SelfService.ServerAPI"));
            builder.Services.AddScoped<IBillsRepository, BillsRepository>();
            builder.Services.AddScoped<ICacheManager, LocalStroageCacheManager>();
            builder.Services.AddMsalAuthentication(options =>
            {
                builder.Configuration.Bind("AzureAdB2C", options.ProviderOptions.Authentication);
                options.ProviderOptions.DefaultAccessTokenScopes.Add("https://sairamaapps.onmicrosoft.com/0a080a72-57eb-4bd3-abe9-efc89389a1b8/user_impersonation");
            });

            //builder.Services.AddAuthorizationCore(options => options.AddAppPolicies());
            builder.Services.AddMatToaster(config =>
                            {
                                config.Position = MatToastPosition.TopCenter;
                                config.PreventDuplicates = true;
                                config.NewestOnTop = true;
                                config.ShowCloseButton = true;
                                config.MaximumOpacity = 95;
                                config.VisibleStateDuration = 3000;
                            });
            builder.Services.AddBlazoredLocalStorage(config =>
        config.JsonSerializerOptions.WriteIndented = true);
            await builder.Build().RunAsync();
        }
    }
}
