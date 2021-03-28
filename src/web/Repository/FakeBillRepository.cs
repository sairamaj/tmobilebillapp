using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq;
using web.Shared.Model;

namespace web.Repository
{
    internal class FakeBillRepository : IBillRepository
    {
        public async Task<IEnumerable<BillDetail>> GetBillDetails(string yearMonth)
        {
            var users = await this.GetUsers();
            return (await GetBillDetailsFromApi(yearMonth)).Select(b =>
            {
                var foundUser = users.FirstOrDefault(u => u.Phone == b.Number);
                if (foundUser != null)
                {
                    b.Name = foundUser.Name;
                }
                else
                {
                    b.Name = $"Not Found";
                }

                return b;
            });
        }

        public Task<IEnumerable<Bill>> GetBills()
        {
            return Task.FromResult<IEnumerable<Bill>>(new List<Bill>{
                new Bill{
                    Type = "Summary_Jan2020",
                    Total = 232.00m,
                    PerLine = 19.99m
                }
            });
        }

        public async Task<IEnumerable<User>> GetUsers()
        {
            return await Task.FromResult<IEnumerable<User>>(new List<User>{
                new User{
                    Name = "User 1",
                    Phone = "(503) 111-1111"
                },
                new User{
                    Name = "User 2",
                    Phone = "(503) 222-2222"
                }
            });
        }

        public Task<IEnumerable<BillDetail>> GetBillDetailsFromApi(string yearMonth)
        {
            return Task.FromResult<IEnumerable<BillDetail>>(new List<BillDetail>{
                new BillDetail{
                    Number = "(503) 111-1111",
                    Total = 34.00m,
                    Equipment = 1.0m,
                    OneTimeCharge = 2.0m,
                    PlanAmount = 19.00m,
                    Services = 3.0m,
                    Type = "Summary_(503) 111-1111"
                },
                new BillDetail{
                    Number = "(503) 222-2222",
                    Total = 34.00m,
                    Equipment = 1.0m,
                    OneTimeCharge = 2.0m,
                    PlanAmount = 19.00m,
                    Services = 3.0m,
                    Type = "Summary_(503) 222-2222"
                },
                new BillDetail{
                    Number = "(503) 333-3333",
                    Total = 34.00m,
                    Equipment = 1.0m,
                    OneTimeCharge = 2.0m,
                    PlanAmount = 19.00m,
                    Services = 3.0m,
                    Type = "Summary_(503) 333-3333"
                }
            });
        }

        public Task<IEnumerable<PrimaryContact>> GetPrimaryContacts()
        {
            throw new System.NotImplementedException();
        }
    }
}