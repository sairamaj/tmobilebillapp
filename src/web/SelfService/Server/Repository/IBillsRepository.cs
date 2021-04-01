using System.Collections.Generic;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Server.Repository
{
    public interface IBillsRepository
    {
        Task<IEnumerable<Bill>> GetBills();
    }
}