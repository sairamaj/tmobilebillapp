using System.Collections.Generic;
using System.Threading.Tasks;
using web.Shared.Model;

namespace web.Repository
{
    internal interface IBillRepository
    {
       Task<IEnumerable<User>> GetUsers(); 
       Task<IEnumerable<Bill>> GetBills();
       Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth);
       Task<IEnumerable<PrimaryContact>> GetPrimaryContacts();
       Task<string> GetDownloadLink(string yearMonth);
    }
}