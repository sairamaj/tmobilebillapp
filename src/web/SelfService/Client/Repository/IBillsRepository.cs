using System.Collections.Generic;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Client.Repository
{
    internal interface IBillRepository
    {
        Task<IEnumerable<Bill>> GetBills();
    }
}