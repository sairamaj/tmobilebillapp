using SelfService.Shared;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SelfService.Server.Repository;

namespace SelfService.Server.Controllers
{
    [Authorize]
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
    }
}