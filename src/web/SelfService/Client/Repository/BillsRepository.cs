using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Client.Repository
{
    internal class BillsRepository : IBillsRepository
    {
        private readonly ICacheManager cacheManager;
        private readonly IHttpClientFactory clientFactory;

        public BillsRepository(IHttpClientFactory clientFactory, ICacheManager cacheManager)
        {
            this.clientFactory = clientFactory ?? throw new ArgumentNullException(nameof(clientFactory));
            this.cacheManager = cacheManager ?? throw new ArgumentNullException(nameof(cacheManager));
        }

        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<BillDetail>>(
                           $"bills-details-{yearMonth}",
                           Constants.BillDetailsCacheExpiry,
                           async () =>
                       {
                           return await this.Client.GetFromJsonAsync<IEnumerable<BillDetail>>($"/api/bills/{yearMonth}");
                       });
        }

        public async Task<IEnumerable<Bill>> GetBills()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<Bill>>(
                           "bills",
                           Constants.BillCacheExpiry,
                           async () =>
                       {
                           return await this.Client.GetFromJsonAsync<IEnumerable<Bill>>("/api/bills");
                       });
        }

        public async Task<Link> GetDownloadLink(string yearMonth)
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<Link>(
                           $"bills-download-url-{yearMonth}",
                           Constants.BillDetailsCacheExpiry,
                           async () =>
                       {
                           return await this.Client.GetFromJsonAsync<Link>($"/api/links/bills/{yearMonth}");
                       });
        }

        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<PrimaryContact>>(
                          $"primary-contacts",
                          Constants.UsersCacheExpiry,
                          async () =>
                      {
                          return await this.Client.GetFromJsonAsync<IEnumerable<PrimaryContact>>($"/api/primarycontacts");
                      });
        }

        public async Task<IEnumerable<User>> GetUsers()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<User>>(
                          $"users",
                          Constants.BillDetailsCacheExpiry,
                          async () =>
                      {
                          return await this.Client.GetFromJsonAsync<IEnumerable<User>>($"/api/users");
                      });
        }

        // Temporary method till we implement full client authorization roles
        // This will throw Un authorized(403) if user is not authorized.
        public async Task EnsureAuthorized()
        {
            await Task.Delay(0);
            // await this.Client.GetFromJsonAsync<bool>("/api/authorized/state");
        }

        public Task<IDictionary<string, Role>> GetUserRoles()
        {
            throw new NotImplementedException("We dont need at client side now.");
        }

        public async Task<IEnumerable<Payment>> GetPayments()
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<Payment>>(
                          $"payments",
                          Constants.PaymentsCacheExpiry,
                          async () =>
                      {
                          return await this.Client.GetFromJsonAsync<IEnumerable<Payment>>($"/api/payments");
                      });
        }

        public async Task<IEnumerable<MonthlyPayment>> GetMonthlyPayments(string yearMonth)
        {
            await this.EnsureAuthorized();
            return await this.cacheManager.GetWithSet<IEnumerable<MonthlyPayment>>(
                          $"monthly_payments_{yearMonth}",
                          Constants.PaymentsCacheExpiry,
                          async () =>
                      {
                          return await this.Client.GetFromJsonAsync<IEnumerable<MonthlyPayment>>($"/api/payments/{yearMonth}");
                      });
        }

        public async Task<IEnumerable<Resource>> GetResources(string name)
        {
            return await this.cacheManager.GetWithSet<IEnumerable<Resource>>(
                            $"resources_{name}",
                          Constants.ResourcesExpiry,
                          async () =>
                      {
                          return await this.Client.GetFromJsonAsync<IEnumerable<Resource>>($"/api/bills/resources/{name}");
                      });
        }

        private HttpClient Client
        {
            get
            {
                return this.clientFactory.CreateClient("TMobile.ServerAPI");
            }
        }

    }
}