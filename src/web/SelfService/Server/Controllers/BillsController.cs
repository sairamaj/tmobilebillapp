using SelfService.Shared;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SelfService.Server.Repository;

namespace SelfService.Server.Controllers
{
    [Authorize(Roles = "Users")]
    [ApiController]
    [Route("[controller]")]
    public class BillsController
    {
        private readonly IBillsRepository repository;

        public BillsController(IBillsRepository repository)
        {
            this.repository = repository ?? throw new System.ArgumentNullException(nameof(repository));
        }

        [HttpGet]
        [Route("/api/bills")]
        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await this.repository.GetBills();
        }

        [HttpGet]
        [Route("/api/bills/{yearMonth}")]
        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            return await this.repository.GetBillDetails(yearMonth);
        }

        [HttpGet]
        [Route("/api/users")]
        public async Task<IEnumerable<User>> GetUsers()
        {
            return await this.repository.GetUsers();
        }

        [HttpGet]
        [Route("/api/primarycontacts")]
        public async Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            return await this.repository.GetPrimaryContacts();
        }

        [HttpGet]
        [Route("/api/links/bills/{yearMonth}")]
        public async Task<Link> GetBillDownloadLink(string yearMonth)
        {
            System.Console.WriteLine($">>>>> Bill download link:{yearMonth} <<<<");
            return await this.repository.GetDownloadLink(yearMonth);
        }
    }
}