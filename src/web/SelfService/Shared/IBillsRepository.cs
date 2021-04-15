using System.Collections.Generic;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Shared
{
    public interface IBillsRepository
    {
        Task<IEnumerable<User>> GetUsers();
        Task<IEnumerable<PrimaryContact>> GetPrimaryContacts();
        Task<IEnumerable<Bill>> GetBills();
        Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth);
        Task<Link> GetDownloadLink(string yearMonth);
        Task<IDictionary<string,Role>> GetUserRoles();
        Task<IEnumerable<Payment>> GetPayments();
        Task<IEnumerable<MonthlyPayment>> GetMonthlyPayments(string yearMonth);
    }
}