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
    public class PaymentsController
    {
        private readonly IBillsRepository repository;

        public PaymentsController(IBillsRepository repository)
        {
            this.repository = repository ?? throw new System.ArgumentNullException(nameof(repository));
        }

        [HttpGet]
        [Route("/api/payments")]
        public async Task<IEnumerable<Payment>> GetPayments()
        {
            return await this.repository.GetPayments();
        }

        [HttpGet]
        [Route("api/payments/user/{number}")]
        public async Task<IEnumerable<MonthlyPayment>> GetMonthlyPayments(string number)
        {
            return await this.repository.GetMonthlyPayments(number);
        }
        
    }
}