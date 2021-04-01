using System.Collections.Generic;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Server.Repository
{
    class BillsRepository : IBillsRepository
    {
        public async Task<IEnumerable<Bill>> GetBills()
        {
            return await Task.FromResult<IEnumerable<Bill>>(
                new List<Bill>{
             new Bill{
                Type = "Summary_Apr2020",
                PerLine = 10.11m,
                Total = 2.2m
            },
            new Bill{
                Type = "Summary_May2020",
                PerLine = 30.33m,
                Total = 3.3m
            }});

        }
    }
}