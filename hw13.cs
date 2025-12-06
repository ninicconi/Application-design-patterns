using System;

namespace TicketMachineSystem
{
    public interface IState
    {
        void SelectTicket(TicketMachine ctx);
        void InsertMoney(TicketMachine ctx);
        void DispenseTicket(TicketMachine ctx);
        void Cancel(TicketMachine ctx);
    }


    public class TicketMachine
    {
        public IState CurrentState { get; set; }
        public int TicketPrice { get; } = 5;

        public TicketMachine()
        {
            CurrentState = new IdleState();
            Console.WriteLine("[System] Machine Ready. State: Idle");
        }

        public void SelectTicket() => CurrentState.SelectTicket(this);
        public void InsertMoney() => CurrentState.InsertMoney(this);
        public void DispenseTicket() => CurrentState.DispenseTicket(this);
        public void Cancel() => CurrentState.Cancel(this);
    }


    public class IdleState : IState
    {
        public void SelectTicket(TicketMachine ctx)
        {
            Console.WriteLine($"Action: Ticket Selected. Price = ${ctx.TicketPrice}.");
            ctx.CurrentState = new WaitingForMoneyState();
        }

        public void InsertMoney(TicketMachine ctx) =>
            Console.WriteLine("Error: You must select a ticket first.");

        public void DispenseTicket(TicketMachine ctx) =>
            Console.WriteLine("Error: No ticket to dispense.");

        public void Cancel(TicketMachine ctx) =>
            Console.WriteLine("Error: Nothing to cancel.");
    }


    public class WaitingForMoneyState : IState
    {
        public void SelectTicket(TicketMachine ctx) =>
            Console.WriteLine("Ticket already selected.");

        public void InsertMoney(TicketMachine ctx)
        {
            Console.WriteLine("Action: Money Inserted.");
            ctx.CurrentState = new MoneyReceivedState();
        }

        public void DispenseTicket(TicketMachine ctx) =>
            Console.WriteLine("Error: Insert money first.");

        public void Cancel(TicketMachine ctx)
        {
            Console.WriteLine("Action: Transaction Canceled.");
            ctx.CurrentState = new TransactionCanceledState();
        }
    }


    public class MoneyReceivedState : IState
    {
        public void SelectTicket(TicketMachine ctx) =>
            Console.WriteLine("Error: Money already inserted.");

        public void InsertMoney(TicketMachine ctx) =>
            Console.WriteLine("Error: Payment already made.");

        public void DispenseTicket(TicketMachine ctx)
        {
            Console.WriteLine("Action: Ticket Printed. Please take your ticket.");
            ctx.CurrentState = new TicketDispensedState();
        }

        public void Cancel(TicketMachine ctx)
        {
            Console.WriteLine("Action: Transaction Canceled. Money refunded.");
            ctx.CurrentState = new TransactionCanceledState();
        }
    }


    public class TicketDispensedState : IState
    {
        public void SelectTicket(TicketMachine ctx) =>
            Console.WriteLine("Ticket already dispensed.");

        public void InsertMoney(TicketMachine ctx) =>
            Console.WriteLine("Ticket already dispensed.");

        public void DispenseTicket(TicketMachine ctx) =>
            Console.WriteLine("You already received your ticket.");

        public void Cancel(TicketMachine ctx) =>
            Console.WriteLine("Cannot cancel. Transaction is complete.");
    }


    public class TransactionCanceledState : IState
    {
        public void SelectTicket(TicketMachine ctx)
        {
            Console.WriteLine("System resetting...");
            ctx.CurrentState = new IdleState();
        }

        public void InsertMoney(TicketMachine ctx) =>
            Console.WriteLine("Transaction was canceled.");

        public void DispenseTicket(TicketMachine ctx) =>
            Console.WriteLine("Transaction was canceled.");

        public void Cancel(TicketMachine ctx) =>
            Console.WriteLine("Already canceled.");
    }


    class Program
    {
        static void Main(string[] args)
        {
            TicketMachine m = new TicketMachine();

            Console.WriteLine("\n--- Scenario 1: Successful Purchase ---");
            m.SelectTicket();
            m.InsertMoney();
            m.DispenseTicket();

            Console.WriteLine("\n--- Scenario 2: Canceled Transaction ---");
            m.CurrentState = new IdleState(); 
            m.SelectTicket();
            m.Cancel();
            m.DispenseTicket();

            Console.ReadKey();
        }
    }
}
