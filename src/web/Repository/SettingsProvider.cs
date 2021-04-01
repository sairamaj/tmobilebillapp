using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using web.Shared.Model;

namespace web.Repository
{
    class SettingsProvider: ISettingsProvider
    {
        private readonly IOptions<UrlConfig> urlConfigOptions;

        public SettingsProvider(IOptions<UrlConfig> urlConfigOptions)
        {
            this.urlConfigOptions = urlConfigOptions ?? throw new ArgumentNullException(nameof(urlConfigOptions));
        }

        public string GetBillDetailsUrl(string yearMonth)
        {
            return string.Format(urlConfigOptions.Value.DetailsUrl,yearMonth);
        }

        public string GetBillsUrl()
        {
            return urlConfigOptions.Value.BillsUrl;
        }

        public string GetDownloadUrl(string yearMonth)
        {
            return string.Format(urlConfigOptions.Value.GetDownloadUrl,yearMonth);
        }

        public string GetUserUrl()
        {
            return urlConfigOptions.Value.Users;
        }
    }
}